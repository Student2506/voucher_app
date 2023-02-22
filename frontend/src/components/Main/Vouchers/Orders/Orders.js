import RadioFake from "../RadioFake/RadioFake";
import React from "react";

export default function Orders({ onSelect, customerOrders }) {
  return (
    <>
      {
        customerOrders.map((order) =>
          <RadioFake
            value={order.order_id}
            key={order.order_id}
            id={order.order_id}
            onChange={onSelect}
            description={order.order_name}
            name={"order"}
          />
        )
      }
    </>
  )
}
