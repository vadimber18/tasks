class SelectMixin:
    def prepare_select_query(self, **kwargs):
        query = self.table.select()
        query = self.prepare_where(query, **kwargs)
        query = self.prepare_order(query, kwargs.get("order"))
        query = self.prepare_pagination(
            query, kwargs.get("limit"), kwargs.get("offset")
        )
        return query

    def prepare_where(self, query, **where):
        for ilike_field in self.ilike_fields:
            if value := where.get(ilike_field):
                query = query.where(
                    getattr(self.table.c, str(ilike_field)).ilike(f"%{value}%")
                )
        for exact_field in self.exact_fields:
            if value := where.get(exact_field):
                query = query.where(getattr(self.table.c, str(exact_field)) == value)
        return query

    def prepare_order(self, query, order):
        if order:
            for order_field in order.split(","):
                query = query.order_by(getattr(self.table.c, order_field))
        return query

    @staticmethod
    def prepare_pagination(query, limit, offset):
        return query.limit(limit).offset(offset)


class InsertMixin:
    ...


class UpdateMixin:
    def prepare_update_query(self, where: dict, values: dict):
        query = self.table.update()
        query = self.prepare_where(query, **where)
        return query.values(**values)

    def prepare_where(self, query, **where):
        for field_name, value in where.items():
            query = query.where(getattr(self.table.c, str(field_name) == value))
        return query
