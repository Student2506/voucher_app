import React, { useEffect, useMemo, useState } from "react";
import RadioFake from "../RadioFake/RadioFake";
import { useDispatch, useSelector } from "react-redux";
import {
  setFilteredCustomers,
  getCustomerOrders,
  toggleCheckedCustomer
} from "../../../../utils/store/customersSlice";

export default React.memo(function Customers() {

  const dispatch = useDispatch();
  const { customers, filteredCustomers } = useSelector(state => state.customers);

  /*Выбор Контрагента, внутри чистим заказы и темплейты, ради избежания мискликов*/
  function handleSelectCustomer(id) {
    dispatch(toggleCheckedCustomer({id}))
    dispatch(getCustomerOrders({id}))
  }

  function filterCustomers(query) {
    const filtred = customers.filter((customer) => {
      return customer.customer_name === query
    });
    dispatch(setFilteredCustomers(filtred));
  }

  const customersArr = useMemo(() => {
    return filteredCustomers ? filteredCustomers : customers;
  }, [filteredCustomers, customers])

  return (
    <form className="vouchers__form_type_customers">
      <fieldset className="vouchers__filed">
        <input className="input input_place_vouchers" placeholder="Фильтр по наименованию..." onChange={(e) => {filterCustomers(e.target.value)}}/>
        <button type={"reset"} className="button button_icon_close button_place_vouchers" />
      </fieldset>
      <div className="customers">
        {
          customersArr.map((customer) =>
            <RadioFake
              onChange={() => {handleSelectCustomer(customer.customer_id)}}
              key={customer.customer_id}
              id={customer.customer_id + 2000}
              description={customer.customer_name}
              name={"customer"}
              defaultChecked={customer.checked}
            />
          )
        }
      </div>
    </form>
  )
}
)
