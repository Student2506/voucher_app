import React from "react";
import RadioFake from "../RadioFake/RadioFake";

export default function Customers({ onSelectCustomer, customersData, onClear }) {
  function handleSelectCustomer(id) {
    onSelectCustomer(id);
    onClear();
  }

  return (
    <div className="customers">
      {
        customersData.map((customer) =>
          <RadioFake
            onClick={() => {handleSelectCustomer(customer.customer_id)}}
            key={customer.customer_id}
            id={customer.customer_id + 2000}
            description={customer.customer_name}
            name={"customer"}
          />
        )
      }
    </div>
  )
}
