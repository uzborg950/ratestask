import datetime as dt
from typing import List

from src.database.db import conn
from src.price.repository.model import PriceRequestDAO
from src.price.service.model import AvgPriceDTO

db = conn.cursor()


def get_avg_price_port_to_slug(price_request_dao: PriceRequestDAO) -> List[AvgPriceDTO]:
    db.execute("""select pr."day" as day, Avg(pr.price) as avg_price, count(pr.price) as count from prices pr 
                    inner join ports p_orig on pr.orig_code  = p_orig.code 
                    inner join ports p_dest on pr.dest_code = p_dest.code
                    where pr.orig_code = %(orig)s and p_dest.parent_slug = %(dest)s
                    and pr."day" >= %(day_from)s and pr."day" <= %(day_to)s
                    group by pr."day" having count(pr.price) >= %(min_sample_size)s
                    order by pr."day" """,
               {"orig": price_request_dao.origin, "dest": price_request_dao.destination,
                "day_from": price_request_dao.date_from, "day_to": price_request_dao.date_to,
                "min_sample_size": price_request_dao.min_sample_size})
    db_results = db.fetchall()
    return [AvgPriceDTO(average_price=round(result[1], 3), day=dt.datetime.combine(result[0], dt.datetime.min.time()),
                        count=result[2]) for result in db_results] if db_results else []
