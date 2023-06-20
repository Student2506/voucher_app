import React, { useMemo } from 'react';
import ListItems from "../../../ListItems/ListItems";
import { useSelector } from "react-redux";

const Orders = ({onClickItem, filterQuery}) => {

  const {orders} = useSelector(state => state.orders);

  const filtredOrders = useMemo(() => orders.filter(order => order.order_name.toUpperCase().includes(filterQuery.toUpperCase())), [filterQuery, orders]);

  return (
    <>
      {
        filtredOrders.map(order =>
          <ListItems
            listName={"orders"}
            key={order.order_items[0].order_item_id}
            uniqueKey={order.order_items[0].order_item_id}
            title={order.order_name}
            value={order.order_items[0].order_item_id}
            onClickItem={onClickItem}
          />)
      }
    </>
  );
};

export default Orders;
