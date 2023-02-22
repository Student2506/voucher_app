import React, { useEffect, useState } from "react";
import RadioFake from "../RadioFake/RadioFake";

export default React.memo(function Customers({ onSelectCustomer, customersData, onClear }) {

  const [customersState, setCustomersState] = useState([]);

  /*Магический эффект, значение по дефолту не работает(((*/
  useEffect(() => {
    setCustomersState(customersData);
  }, [customersData]);

  /*Выбор Контрагента, внутри чистим заказы и темплейты, ради избежания мискликов*/
  function handleSelectCustomer(id) {
    onSelectCustomer(id);
    onClear();
  }

  /*Не централизованный поиск*/
  function handleSearch(e) {
    setCustomersState(customersData.filter((customer) => {
        return customer.customer_name.toUpperCase().includes(e.target.value.toUpperCase()) ? customer : false;
      })
    )
  }

  return (
    <form className="vouchers__form_type_customers">
      <fieldset className="vouchers__filed">
        <input onChange={handleSearch} className="input input_place_vouchers" placeholder="Фильтр по наименованию..."/>
        <button onClick={() => {setCustomersState(customersData)}} type={"reset"} className="button button_icon_close button_place_vouchers" />
      </fieldset>
      <div className="customers">
        {
          customersState.map((customer) =>
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
