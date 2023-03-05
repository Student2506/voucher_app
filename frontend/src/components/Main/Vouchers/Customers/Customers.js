import React, { useEffect, useState } from "react";
import RadioFake from "../RadioFake/RadioFake";
import { useDispatch, useSelector } from "react-redux";
import { getCustomerOrders } from "../../../../utils/store/customersSlice";

export default React.memo(function Customers({ onClear }) {

  const dispatch = useDispatch();
  const customers = useSelector(state => state.customers.customers);

  /*Выбор Контрагента, внутри чистим заказы и темплейты, ради избежания мискликов*/
  function handleSelectCustomer(id) {
    dispatch(getCustomerOrders({id}))
  }

  return (
    <form className="vouchers__form_type_customers">
      <fieldset className="vouchers__filed">
        <input className="input input_place_vouchers" placeholder="Фильтр по наименованию..."/>
        <button type={"reset"} className="button button_icon_close button_place_vouchers" />
      </fieldset>
      <div className="customers">
        {
          customers.map((customer) =>
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
    </form>
  )
}
)
