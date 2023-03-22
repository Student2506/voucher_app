import NavBar from "./NavBar/NavBar";
import Header from "./Header/Header";
import Vouchers from "./Vouchers/Vouchers";
import { Route } from "react-router-dom";
import { NotFound } from "../NotFound/NotFound";
import Sign from "../Sign/Sign";

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
      <Route path={"/nnn"}>
        <Sign />
      </Route>

    </main>
  )
}
