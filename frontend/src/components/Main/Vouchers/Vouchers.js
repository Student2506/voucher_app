import Customers from "./Customers/Customers";
import Templates from "./Templates/Templates";
import Orders from "./Orders/Orders";
import { useSelector } from "react-redux";

export default function Vouchers() {

  const {templates, orders} = useSelector(state => state.customers);

  return (
    <section className="vouchers">
      <Customers />
      <div className="vouchers__main">
        {
          orders.length > 0 ?
            <>
              <article className="vouchers__orders vouchers__block">
                <h2 className="vouchers__title">Заказы</h2>
                <div className="vocuhers__block-container">
                  <Orders />
                </div>
              </article>
              {
                templates.length > 0 ?
                  <article className="vouchers__templates vouchers__block">
                    <h2 className="vouchers__title">Шаблоны</h2>
                    <div className="vocuhers__block-container">
                      <Templates />
                    </div>
                  </article>
                  : <></>
              }
            </>
            : <div className="voucher__nothing"></div>
        }

      </div>
    </section>
  )
}
