import Order from "./Order/Order";
import { useState } from "react";

export default function Vouchers({ customersData, onSelectCustomer, customerOrders, onSelectOrder, orderTemplates, onClear, onSubmit }) {

  const [email, setEmail] = useState('');
  const [orderId, setOrderId] = useState('');
  const [template, setTemplate] = useState('');
  const customerClasses = ['vouchers__customer']


  function handleSelectCustomer(id) {
   onSelectCustomer(id);
   customerClasses.push('voucher__customer_checked');
   onClear();
  }

  function handleSelectOrder(e) {
    onSelectOrder(e.target.value);
    setOrderId(e.target.value);
  }

  function handleSelectTemplate(e) {
    setTemplate(e.target.value);
  }

  function handleSubmit(e) {
    e.preventDefault();
    onSubmit(orderId, template, email);
  }

  return (
    <section className="vouchers">
      <form className="vouchers__form_type_customers">
        <fieldset className="vouchers__filed">
          <input className="input input_place_vouchers" placeholder="Фильтр по наименованию..."/>
          <button type={"reset"} className="button button_icon_close button_place_vouchers" />
        </fieldset>

        <div className="vouchers__customers">
          {
            customersData.map((customer) =>
              <h2 onClick={(e) => {handleSelectCustomer(customer.customer_id)}} key={customer.customer_id} className={customerClasses.join(' ')}>{customer.customer_name}</h2>
            )
          }
        </div>
      </form>
      {
        customerOrders.length > 0 ?
          <div className="vouchers__main">
            <div className="vouchers__orders vouchers__block">
              <h2 className="vouchers__title">Заказы</h2>
              <div className="vocuhers__block-container">
                {
                  customerOrders.map((order) =>
                    <Order
                      type="radio"
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
                {
                  orderTemplates.length > 0 ?
                    <>
                    {
                      orderTemplates.map((template, index) =>
                        <Order
                          type="radio"
                          value={Object.keys(template).map((key) => key)}
                          id={index + 1000}
                          key={index}
                          description={Object.values(template).map((val) => val)}
                          name={"template"}
                          onChange={handleSelectTemplate}
                        />
                      )
                    }
                      <form className="vouchers__form_type_email" onSubmit={handleSubmit}>
                        <fieldset className="vouchers__filed">
                          <input onChange={(e) => {setEmail(e.target.value)}} type="email" className="input input_place_vouchers" placeholder="Введите E-Mail получателя"/>
                          <button type={"reset"} className="button button_icon_close button_place_vouchers" onClick={() => {setEmail('')} }/>
                        </fieldset>
                        <button type="submit" className="button button_theme_blue button_place_vouchers-main">Подтвердить</button>
                      </form>
                    </> : <></>
                }
              </div>
            </div>
          </div>
          : <div className="vouchers__nothing"></div>
      }
    </section>
  )
}
