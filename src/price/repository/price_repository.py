import datetime as dt
from typing import List

from src.database.db import conn
from src.price.repository.model import PriceRequestDAO
from src.price.service.model import AvgPriceDTO

db = conn.cursor()


def get_avg_price(price_request_dao: PriceRequestDAO) -> List[AvgPriceDTO]:
    if not price_request_dao.origins or not price_request_dao.destinations:
        return []
    db.execute("""select pr."day" as day, Avg(pr.price) as avg_price, count(pr.price) as count 
                    from prices pr 
                    where pr.orig_code in %(orig)s and pr.dest_code in %(dest)s
                    and pr."day" >= %(day_from)s and pr."day" <= %(day_to)s
                    group by pr."day" having count(pr.price) >= %(min_sample_size)s
                    order by pr."day" """,
               {"orig": tuple([origin for origin in price_request_dao.origins]), "dest": tuple([destination for destination in price_request_dao.destinations]),
                "day_from": price_request_dao.date_from, "day_to": price_request_dao.date_to,
                "min_sample_size": price_request_dao.min_sample_size})
    db_results = db.fetchall()
    return [AvgPriceDTO(average_price=round(result[1], 2), day=dt.datetime.combine(result[0], dt.datetime.min.time()),
                        count=result[2]) for result in db_results] if db_results else []
