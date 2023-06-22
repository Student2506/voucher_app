import {createSlice, createAsyncThunk} from "@reduxjs/toolkit";
import { BASE_URL } from "../../constants";

export const getVouchers = createAsyncThunk(
  'voucherDate/getVouchers',
  async function({ barcode, order }, {dispatch, getState, rejectWithValue}) {
    const jwt = getState().user.userData.jwt.auth;
    try {
      const res = await fetch(`${BASE_URL}/api/v1/stocks/?stock_strbarcode=${barcode}&client_order_item__order_id__order_id=${order}`, {
        method: 'GET',
        headers: {
          "Authorization": `JWT ${jwt}`
        }
      })
      if (!res.ok) throw new Error(`Ошибка при получении данных`);
      const data = await res.json();
      const dataWithChecked = data.results.map((item) => {
        return {
          ...item,
          checked: false,
        }
      })
      dispatch(addVouchers(dataWithChecked))
    } catch (err) {
      return rejectWithValue(err.message);
    }
  }
)

export const updateExpiryDate = createAsyncThunk(
  'voucherDate/pushNewExpiryDate',
  async function ({ date, barcodes }, {dispatch, getState, rejectWithValue}) {
    const jwt = getState().user.userData.jwt.auth;
    try {
      const res = await fetch(`${BASE_URL}/api/v1/extend_vouchers/`, {
        method: 'PUT',
        headers: {
          "Authorization": `JWT ${jwt}`,
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          "codes": barcodes,
          "extend_date": date,
        })
      })
      if (!res.ok) throw new Error(`Ошибка при получении данных`);
      const data = await res.json();
      dispatch(updateVouchers(data))
    } catch (e) {
      rejectWithValue(e);
    }
  }
)

export const changeDateSlice = createSlice({
  name: 'voucherDate',
  initialState: {
    vouchers: [],
    status: null,
  },
  reducers: {
    addVouchers(state, action) {
      state.vouchers = action.payload;
    },
    selectVoucher(state, action) {
      const selectedVoucher = state.vouchers.find((voucher) => voucher.stock_strbarcode === action.payload);
      selectedVoucher.checked = !selectedVoucher.checked;
    },
    selectVouchers(state, action) {
      // const selectedVouchers = state.vouchers.filter((voucher) => {
      //   let selected = false;
      //   for(let i = 0; i<action.payload.barcodes.length; i++) {
      //     if (voucher.stock_strbarcode === action.payload.barcodes[i]) {
      //       selected = true;
      //     }
      //   }
      //   return selected;
      // })
      // selectedVouchers.forEach((el) => {
      //   el.checked = action.payload.checked
      // })
      state.vouchers.forEach((item) => {
        item.checked = action.payload.checked;
      })
    },
    updateVouchers(state, action) {
      const selectedVouchers = state.vouchers.filter((voucher) => voucher.checked);
      selectedVouchers.forEach((voucher) => {
        voucher.expiry_date = action.payload[0].expiry_date;
      })
    }
  },
  extraReducers: {
    [updateExpiryDate.pending]: (state) => {
      state.status = 'loading-date'
    },
    [updateExpiryDate.rejected]: (state) => {
      state.status = 'rejected'
    },
    [updateExpiryDate.fulfilled]: (state) => {
      state.status = 'resolved'
    },
    [getVouchers.pending]: (state) => {
      state.status = 'loading'
    },
    [getVouchers.rejected]: (state) => {
      state.status = 'rejected'
    },
    [getVouchers.fulfilled]: (state) => {
      state.status = null;
    },
  }
})

export const {addVouchers, updateVouchers, selectVoucher, selectVouchers} = changeDateSlice.actions;

export default changeDateSlice.reducer;
