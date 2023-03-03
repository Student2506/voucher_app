import RadioFake from "../RadioFake/RadioFake";
import React from "react";
import { useDispatch, useSelector } from "react-redux";
import { getOrderTemplates } from "../../../../store/customersSlice";

export default function Orders() {

  const dispatch = useDispatch();
  const orders = useSelector(state => state.customers.orders)

  return (
    <>
      {
        orders.map((order) =>
          <RadioFake
            value={order.order_id}
            key={order.order_id}
            id={order.order_id}
            onChange={(e) => {dispatch(getOrderTemplates(e.target.value))}}
            description={order.order_name}
            name={"order"}
          />
        )
      }
    </>
  )
}
