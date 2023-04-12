import {createSlice, createAsyncThunk} from "@reduxjs/toolkit";
import { baseUrl } from "../../constants";
import { fulfilledFetch, pendingFetch, rejectFetch } from "./statusAppSlice";

export const getVouchers = createAsyncThunk(
  'voucherDate/getVouchers',
  async function(_, {dispatch, getState}) {
    const jwt = getState().user.userData.jwt.auth;
    dispatch(pendingFetch());
    try {
      const res = await fetch(`${baseUrl}/api/v1/stocks/`, {
        method: 'GET',
        headers: {
          "Authorization": `JWT ${jwt}`
        }
      })
      if (!res.ok) throw new Error(`Ошибка при получении данных`);
      const data = await res.json();
      dispatch(addVouchers({data: data.results}));
      dispatch(fulfilledFetch())
    } catch (e) {
      dispatch(rejectFetch());
    }
  }
)

export const pushNewExpiryDate = createAsyncThunk(
  'voucherDate/pushNewExpiryDate',
  async function (date, {dispatch, getState}) {
    const jwt = getState().user.userData.jwt.auth;
    const checkedVoucher = getState().changeDate.vouchers.find(voucher => voucher.checked === true)
    try {
      const res = await fetch(`${baseUrl}/api/v1/extend_vouchers/`, {
        method: 'PUT',
        headers: {
          "Authorization": `JWT ${jwt}`,
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          "codes": [checkedVoucher.stock_strbarcode],
          "extend_date": date,
        })
      })
      if (!res.ok) throw new Error(`Ошибка при получении данных`);
      const data = await res.json();
      dispatch(updateVouchers({ data: data }))
    } catch (e) {
      console.log(e);
    }
  }
)

export const changeDateSlice = createSlice({
  name: "voucherDate",
  initialState: {
    vouchers: [],
    checkedVoucher: {},
  },
  reducers: {
    addVouchers(state, action) {
      state.vouchers = action.payload.data.map((item) => {
        return {
          ...item,
          order_id: item.order_id === null ? 0 : item.order_id,
          "checked": false,
        }
      });
    },
    chooseVoucher(state, action) {
      state.vouchers.forEach((item) => {item.checked = false});
      const checkedVoucher = state.vouchers.find(voucher => voucher.stock_strbarcode === action.payload.stock_strbarcode);
      checkedVoucher.checked = true;
      state.checkedVoucher = checkedVoucher;
    },
    updateVouchers(state, action) {
      const date = action.payload.data[0].expiry_date;
      const editedVoucher = state.vouchers.find((voucher) => voucher.stock_strbarcode === action.payload.data[0].stock_strbarcode);
      editedVoucher.expiry_date = date;
    }
  }
})

export const {addVouchers, chooseVoucher, updateVouchers} = changeDateSlice.actions;

export default changeDateSlice.reducer;
