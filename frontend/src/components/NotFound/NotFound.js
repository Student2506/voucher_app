import notFoundLogo from '../../images/not_found.svg';
import { Link } from "react-router-dom";

export function NotFound() {
  return (
    <div className={"notFound"}>
      <img src={notFoundLogo} className="notFound__image"/>
      <p className="notFound__caption">Упс... Похоже такой страницы не существует :(</p>
      <Link to={'/vouchers'} className={"notFound__link"}>Назад</Link>
    </div>
  )
}
