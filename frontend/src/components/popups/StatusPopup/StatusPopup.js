import failureImage from '../../../images/fail.png';
import { useDispatch, useSelector } from "react-redux";
import { clearError } from "../../../utils/store/statusAppSlice";
import { toggleCheckedCustomer } from "../../../utils/store/customersSlice";

export function StatusPopup() {

  const dispatch = useDispatch();
  const {status} = useSelector(state => state.status);

  function handleClose() {
    dispatch(clearError());
    dispatch(toggleCheckedCustomer({id: null}));
  }

  return(
    <div className={`statusPopup ${status === "rejected" ? "statusPopup_opened" : ""}`}>
      <div className="statusPopup__overlay" />
      <div className={"statusPopup__container"}>
        <img src={failureImage} className="statusPopup__image"/>
        <p className="statusPopup__caption">{`Упс... Произошла ошибка, попробуйте еще раз`}</p>
        <button className="button button_icon_close button_place_statusPopup" onClick={handleClose} />
      </div>
    </>
)
}
