import React from 'react';
import account from '../../styles/account.scss';
import { useSelector } from "react-redux";

const Account = ({ extraClass }) => {
  const { login } = useSelector(state => state.user.userData)
  return (
    <div className={`account ${extraClass}`}>
      <p className={"account__name"}>{login}</p>
    </div>
  );
};

export default Account;
