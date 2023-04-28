import React from 'react';
import notFoundLogo from '../../images/not_found.svg';
import { Link } from "react-router-dom";
import styles from '../../styles/notFound.scss';

const NotFound = ({text}) => {
  return (
    <div className={"notFound"}>
      <img src={notFoundLogo} className="notFound__image"/>
      <p className="notFound__caption">{text}</p>
      <Link to={'/vouchers'} className={"notFound__link"}>Назад</Link>
    </div>
  );
};

export default NotFound;
