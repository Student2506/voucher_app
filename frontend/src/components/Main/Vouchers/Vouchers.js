import RadioFake from "./RadioFake/RadioFake";
import React, { useEffect, useState } from "react";
import Customers from "./Customers/Customers";
import Templates from "./Templates/Templates";

export default function Vouchers({ customersData, onSelectCustomer, customerOrders, onSelectOrder, orderTemplates, onClear, onSubmit, preload, success }) {

  const [orderId, setOrderId] = useState('');
  const [customersState, setCustomersState] = useState([]);

  /* Загадка, но работает только так... */
  useEffect(() => {
    setCustomersState(customersData);
  },[customersData])

  function handleSelectOrder(e) {
    onSelectOrder(e.target.value);
    setOrderId(e.target.value);
  }

  function handleSearch(e) {
    setCustomersState(customersData.filter((customer) => {
        return customer.customer_name.toUpperCase().includes(e.target.value.toUpperCase()) ? customer : false;
    })
    )
  }

  console.log(customersState);

  return (
    <section className="vouchers">
      <form className="vouchers__form_type_customers">
        <fieldset className="vouchers__filed">
          <input onChange={handleSearch} className="input input_place_vouchers" placeholder="Фильтр по наименованию..."/>
          <button onClick={() => {setCustomersState(customersData)}} type={"reset"} className="button button_icon_close button_place_vouchers" />
        </fieldset>
        <Customers onSelectCustomer={onSelectCustomer} customersData={customersState} onClear={onClear} />
      </form>
      {
        customerOrders.length > 0 ?
          <div className="vouchers__main">
            <div className="vouchers__orders vouchers__block">
              <h2 className="vouchers__title">Заказы</h2>
              <div className="vocuhers__block-container">
                {/*
                 * Рисую заказы customer'а
                */}
                {
                  customerOrders.map((order) =>
                    <RadioFake
                      value={order.order_id}
                      key={order.order_id}
                      id={order.order_id}
                      onChange={handleSelectOrder}
                      description={order.order_name}
                      name={"order"}
                    />
                  )
                }
              </div>
            </div>
            <div className="vouchers__templates vouchers__block">
              <h2 className="vouchers__title">Шаблоны</h2>
              <div className="vocuhers__block-container">
                {/*
                * Рисую шаблоны для выбранного заказа
                * Форма отправки внутри компонента
                */}
                {
                  orderTemplates.length > 0
                    ?  <Templates
                    orderTemplates={orderTemplates}
                    orderId={orderId}
                    onSubmit={onSubmit}
                    preload={preload}
                    success={success}
                    />
                    : <></>
                }
              </div>
            </div>
          </div>
          : <div className="vouchers__nothing"></div>
      }
    </section>
  )
}
