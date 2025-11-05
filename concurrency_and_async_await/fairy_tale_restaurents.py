# :)

class Burgers:
    # function definition
    async def get_burgers(self, current_order: int, your_order_no: int) -> bool:
        # TODO
        # do some stuff...
        burger_is_ready = False
        if current_order > your_order_no:
            return burger_is_ready
        else:
            if current_order == your_order_no:
                burger_is_ready = True
                return burger_is_ready
            else:
                return burger_is_ready