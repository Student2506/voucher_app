import NavBar from "./NavBar/NavBar";
import Header from "./Header/Header";
import Vouchers from "./Vouchers/Vouchers";

export default function Main({ customersData, onSelectCustomer }) {
  return (
    <main className="main">
      <Header />
      <NavBar />
      <Vouchers customersData={customersData} onSelectCustomer={onSelectCustomer} />
    </main>
  )
}
