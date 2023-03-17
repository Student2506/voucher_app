import RadioFake from "../../../RadioFake/RadioFake";
import React from "react";
import { useDispatch, useSelector } from "react-redux";
import { getOrderTemplates } from "../../../../utils/store/customersSlice";

export default function Orders() {

  const dispatch = useDispatch();
  const orders = useSelector(state => state.customers.orders)

  return (
    <>
      {
        orders.map((order) =>
          <RadioFake
            value={order.order_items[0].order_item_id}
            key={order.order_items[0].order_item_id}
            id={order.order_items[0].order_item_id}
            onChange={(e) => {dispatch(getOrderTemplates({id: e.target.value}))}}
            description={order.order_name}
            name={"order"}
          />
        )
      }
    </>
  )
}
