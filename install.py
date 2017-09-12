"""Install

"""
from app import app
from app import db
from app.models.company import Company, CompanyMeta
from app.models.portfolio import Portfolio, PortfolioEvent
from app.models.quote import Quote

if __name__ == '__main__':
    app.logger.info('Runing Installer')
    db.create_all()
