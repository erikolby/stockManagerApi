import graphene
from graphene_django import DjangoObjectType

from portfoliomanagerapi.models import Stock, Portfolio, Trade

# Object types
class StockType(DjangoObjectType):
    class Meta:
        model = Stock
        fields = ("id", "symbol", "name")

class PortfolioType(DjangoObjectType):
    class Meta:
        model = Portfolio
        fields = ("id", "name", "description", "initialAccountBalance", "accountBalance", "trades")

class TradeType(DjangoObjectType):
    class Meta: 
        model = Trade
        fields = ("id", "stockSymbol", "price", "volume", "portfolio", "tradeOperation")

# Queries
class Query(graphene.ObjectType):
    all_portfolios = graphene.List(PortfolioType)
    portfolio_by_id = graphene.Field(PortfolioType, id=graphene.String(required=True))
    all_stocks = graphene.List(StockType)
    stock_by_symbol = graphene.Field(StockType, symbol=graphene.String (required=True))

    def resolve_all_portfolios(root, info):
        return Portfolio.objects.all()

    def resolve_portfolio_by_id(root, info, id):
        try: 
            return Portfolio.objects.get(id=id)
        except Portfolio.DoesNotExist:
            return None

    def resolve_all_stocks(root, info):
        return Stock.objects.all()

    def resolve_stock_by_symbol(root, info, symbol):
        try:
            return Stock.objects.get(symbol=symbol)
        except Stock.DoesNotExist:
            return None

# Mutations
class CreatePortfolio(graphene.Mutation):
    portfolio = graphene.Field(PortfolioType)

    class Arguments:
        name = graphene.String(required=True)
        description = graphene.String()
        initialAccountBalance = graphene.Int(required=True)

    def mutate(self, info, **kwargs):
        # The account balance on creation is equal to the initial account balance
        accountBalance = kwargs.get("initialAccountBalance")
        
        portfolio = Portfolio(name=kwargs.get("name"), description=kwargs.get("description"), initialAccountBalance=accountBalance, accountBalance=accountBalance)

        portfolio.save()
        return CreatePortfolio(portfolio=portfolio)

class DeletePortfolio(graphene.Mutation):
    portfolio_id = graphene.Int()

    class Arguments:
        portfolio_id = graphene.Int(required=True)

    def mutate(self, info, portfolio_id):
        portfolio = Portfolio.objects.get(id=portfolio_id)

        portfolio.delete()

        return DeletePortfolio(portfolio_id=portfolio_id)

class UpdatePortfolio(graphene.Mutation):
    portfolio = graphene.Field(PortfolioType)

    class Arguments:
        portfolio_id = graphene.Int(required=True)
        name = graphene.String()
        description = graphene.String()

    def mutate(self, info, portfolio_id, name=None, description=None):
        portfolio = Portfolio.objects.get(id=portfolio_id)

        portfolio.name = name if name != None and name != "" else portfolio.name
        portfolio.description = description if description != None else portfolio.description

        portfolio.save()
        
        return UpdatePortfolio(portfolio=portfolio) 

# Enum defining trade option
class BuySellOption(graphene.Enum):
    BUY = "BUY"
    SELL = "SELL"

class BuyStock(graphene.Mutation):
    trade = graphene.Field(TradeType)

    class Arguments:
        portfolio_id = graphene.Int(required=True)
        symbol = graphene.String(required=True)
        price = graphene.Int(required=True)
        volume = graphene.Int(required=True)

    def mutate(self, info, **kwargs):
        portfolio = Portfolio.objects.get(id=kwargs.get("portfolio_id"))
        tradePrice = kwargs.get("price")

        # Not enough balance to buy the stocks
        if (portfolio.accountBalance < tradePrice):
            return None

        # Update the account balance
        portfolio.accountBalance -= tradePrice
        portfolio.save()
        
        trade = Trade(stockSymbol=kwargs.get("symbol"), volume=kwargs.get("volume"), tradeOperation=BuySellOption.BUY, price=tradePrice, portfolio=portfolio)
        
        trade.save()        

        return BuyStock(trade=trade)
        
class SellStock(graphene.Mutation):
    trade = graphene.Field(TradeType)

    class Arguments:
        portfolio_id = graphene.Int(required=True)
        symbol = graphene.String(required=True)
        price = graphene.Int(required=True)
        volume = graphene.Int(required=True)

    def mutate(self, info, **kwargs):
        portfolio = Portfolio.objects.get(id=kwargs.get("portfolio_id"))
        portfolioTrades = Trade.objects.filter(portfolio__name=portfolio.name)
        volume = kwargs.get("volume")
        stockSymbol = kwargs.get("symbol")
        tradePrice = kwargs.get("price")

        # Check if the current portfolio have enough volume of the stock to trade
        totalVolume = 0
        for trade in portfolioTrades:
            if (trade.stockSymbol == stockSymbol):
                if ("BUY" in trade.tradeOperation):
                    totalVolume += trade.volume
                else:
                    totalVolume -= trade.volume

        # The portfolio does not have the required volume                
        if (volume > totalVolume):
            return None

        portfolio.accountBalance += tradePrice
        portfolio.save()

        # Confirm the sell option and update the portfolio
        trade = Trade(stockSymbol=kwargs.get("symbol"), volume=kwargs.get("volume"), tradeOperation=BuySellOption.SELL, price=tradePrice, portfolio=portfolio)

        trade.save()

        return SellStock(trade=trade)


class Mutation(graphene.ObjectType):
    create_portfolio = CreatePortfolio.Field()
    delete_portfolio = DeletePortfolio.Field()
    update_portfolio = UpdatePortfolio.Field()
    buy_stock = BuyStock.Field()
    sell_stock = SellStock.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)