import NavBar from "./NavBar/NavBar";
import Header from "./Header/Header";
import Vouchers from "./Vouchers/Vouchers";

export default function Main(props) {
  return (
    <main className="main">
      <Header />
      <NavBar />
      <Vouchers
        {...props}
      />
    </main>
  )
}
