export default function Vouchers({ customersData, onSelectCustomer }) {

  function handleSelectCustomer(e) {
   onSelectCustomer(e.target.value);
  }

  return (
    <section className="vouchers">
      <form className="vouchers__form">
        <label htmlFor="voucher_customer">Выберите контрагента</label>
        <select className="vouchers__select" name="voucher_customer" id="voucher_customer" onChange={handleSelectCustomer}>
          {
            customersData.map((customer, index) => <option key={index} value={customer.customer_id}>{customer.customer_name}</option> )
          }
        </select>
      </form>
    </section>
  )
}
