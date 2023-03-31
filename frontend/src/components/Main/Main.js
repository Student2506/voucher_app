import NavBar from "./NavBar/NavBar";
import Header from "./Header/Header";
import Vouchers from "./Vouchers/Vouchers";
import { Route } from "react-router-dom";
import Refund from "./Refund/Refund";
import VoucherTime from "./VoucherTime/VoucherTime";

export default function Main(props) {
  return (
    <main className="main">
      <Header />
      <NavBar />
      <Route path={"/vouchers"}>
        <Vouchers
          {...props}
        />
      </Route>
      <Route path="/refund">
        <Refund />
      </Route>
      <Route path="/time-management">
        <VoucherTime />
      </Route>
    </main>
  )
}
