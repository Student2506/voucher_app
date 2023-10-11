import React, { useCallback, useState } from 'react';
import SearchInput from "../../../SearchInput/SearchInput";
import StatusSpan from "../../../StatusSpan/StatusSpan";
import {FIRST_EMAIL_FIELD_INDEX, MAX_EMAIL_FIELDS_COUNT} from "../../../../constants";
import { useSelector } from "react-redux";

const SubmitForm = ({onSubmit, changeInputValue, clearInputValue, disabled, share}) => {

  const [emailFieldsCount, setEmailFieldsCount] = useState([FIRST_EMAIL_FIELD_INDEX]);

  const {pushStatus} = useSelector(state => state.orders);

  /*Функция добавления нового инпута*/
  const addEmailField = () => {
    if (emailFieldsCount.length < MAX_EMAIL_FIELDS_COUNT) {
      setEmailFieldsCount([...emailFieldsCount, emailFieldsCount[emailFieldsCount.length - 1] + 1]);
    }
  };

  const removeEmailField = () => {
    if (emailFieldsCount.length !== 1) {
      const i = emailFieldsCount.map((j) => j);
      i.pop();
      setEmailFieldsCount(i);
    }
  }

  /*Функция рендера полей ввода*/
  const renderEmailFields = useCallback(() => {
    return emailFieldsCount.map((i) => (
        <SearchInput
          key={i}
          type="email"
          required={true}
          placeholder="Введите email получателя"
          name={`email-${i}`}
          onChangeInput={changeInputValue}
          onClickButton={() => clearInputValue(i)}
        />
    ));
  }, [changeInputValue, clearInputValue, emailFieldsCount]);

  return (
    <form className={"vouchers__submit"} onSubmit={onSubmit}>
      <div className={"vouchers__submit_input-container"}>
        {renderEmailFields()}
        <button
          className="button vouchers__submit_add"
          type="button"
          onClick={addEmailField}
          aria-label="Добавить еще одно поле для ввода email"
        />
        <button type={"button"} className={"button vouchers__remove-input-btn"} onClick={removeEmailField}/>
      </div>
      <StatusSpan status={pushStatus} rejectedMessage={"Упс, что-то пошло не так..."} resolvedMessage={"Сертификаты успешно высланы на почту"}/>
      <button disabled={disabled} type={"submit"} className={`button button_theme_blue vouchers__submit_button`}>Подтвердить</button>
    </form>
  );
};

export default SubmitForm;
