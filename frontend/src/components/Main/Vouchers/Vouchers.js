import RadioFake from "./RadioFake/RadioFake";
import React, { useEffect, useState } from "react";
import Customers from "./Customers/Customers";
import Templates from "./Templates/Templates";
import Orders from "./Orders/Orders";

export default function Vouchers({
                                   customersData,
                                   onSelectCustomer,
                                   customerOrders,
                                   // onSelectOrder,
                                   orderTemplates,
                                   onClear,
                                   onSubmit,
                                   preload,
                                   success }) {

  // const [orderId, setOrderId] = useState('');

  /*Выбор заказа, приводит к запрос на темплейты*/
  // function handleSelectOrder(e) {
  //   onSelectOrder(e.target.value);
  //   setOrderId(e.target.value);
  // }

  return (
    <section className="vouchers">
      <Customers />
          <div className="vouchers__main">
            <article className="vouchers__orders vouchers__block">
              <h2 className="vouchers__title">Заказы</h2>
              <div className="vocuhers__block-container">
                <Orders />
              </div>
            </article>
                  <article className="vouchers__templates vouchers__block">
                    <h2 className="vouchers__title">Шаблоны</h2>
                    <div className="vocuhers__block-container">
                      <Templates />
                    </div>
                  </article>
          </div>
    </section>
  )
}
