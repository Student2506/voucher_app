import React from 'react';
import { useSelector } from "react-redux";

const TableItems = ({vouchers, onChange}) => {

  return (
    <div className={"change__table_items"}>
      {
        vouchers.map(voucher =>
          <label className={`change__table_item ${voucher.checked ? "change__table_item-active" : ""}`} key={voucher.stock_strbarcode}>
            <input type={"checkbox"} checked={voucher.checked} value={voucher.stock_strbarcode} onChange={onChange}/>
            <p className={"change__table_text"}>{voucher.order_id || "Номер заказа отсутсвует"}</p>
            <p className={"change__table_text"}>{voucher.stock_strbarcode}</p>
            <p className={"change__table_text"}>{`${voucher.issued_date.slice(0, -8)} - ${voucher.expiry_date.slice(0, -8)}`}</p>
          </label>
        )
      }
    </div>
  );
};

export default TableItems;
