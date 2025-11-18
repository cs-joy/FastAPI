# Extra Data Types
# Source: https://fastapi.tiangolo.com/tutorial/extra-data-types/

# # # # Up to now, we have been using common data types, like:
'''
- int
- float
- str
- bool
'''

# But we can also use more complex data types
# and we will still have the same features as seen up to now:
'''
- great editor support
- data conversion from incoming requests.
- data conversion for response data.
'''

# # # Other data types
'''
# https://fastapi.tiangolo.com/tutorial/extra-data-types/#other-data-types
- UUID
- datetime.datetime
- datetime.date
- datetime.time
- datetime.timedelta
- frozenset
- bytes
- Decimal

Valid pydantic data types: https://docs.pydantic.dev/latest/usage/types/types/
'''
# Examples
from uuid import UUID
from datetime import datetime, date, time, timedelta

from typing import Annotated
from fastapi import FastAPI, Body
import logfire

app = FastAPI()
logfire.configure()
logfire.instrument_fastapi(app)


@app.put('/products/{product_id}')
async def view_product(
    product_id: UUID,
    start_datetime: Annotated[datetime, Body()],
    end_datetime: Annotated[datetime, Body()],
    process_after: Annotated[timedelta, Body()],
    repeat_at: Annotated[time | None, Body()] = None,
):
    # perform normal date manipulations
    start_process = start_datetime + process_after
    duration = end_datetime - start_process
    return {
        "product_id": product_id,
        "start_datetime": start_datetime,
        "end_datetime": end_datetime,
        "process_after": process_after,
        "repeat_at": repeat_at,
        "start_process": start_process,
        "duration": duration,
    }



