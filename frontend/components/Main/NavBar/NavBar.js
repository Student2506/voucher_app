import { Link } from "react-router-dom";

export default function NavBar() {
  return (
    <aside className="navBar">
      <div className="navBar__logo" />
      <h2 className="navBar__title">Ваучеры</h2>
      <nav className="navBar__navigation">
        <Link to="/vouchers" className="navBar__link navBar__link_current" >Ваучеры</Link>
      </nav>
    </aside>
  )
}
