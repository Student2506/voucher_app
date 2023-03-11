import failureImage from '../../../images/fail.png';
import { useDispatch } from "react-redux";
import { clearError } from "../../../utils/store/statusAppSlice";

export function StatusPopup({error, status}) {

  const dispatch = useDispatch();

  return(
    <div className={`statusPopup ${status === "rejected" ? "statusPopup_opened" : ""}`}>
      <img src={failureImage} className="statusPopup__image"/>
      <p className="statusPopup__caption">{`Упс... Произошла ошибка, попробуйте еще раз ${error}`}</p>
      <button className="button button_icon_close button_place_statusPopup" onClick={() => {dispatch(clearError())}} />
    </div>
  )
}
