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

export const changeDateSlice = createSlice({
  name: "voucherDate",
  initialState: {
    vouchers: [],
    checkedVoucher: {},
  },
  reducers: {
    addVouchers(state, action) {
      state.vouchers = action.payload.data;
    },
    chooseVoucher(state, action) {
      state.checkedVoucher = action.payload;
    }
  }
})

export const {addVouchers, chooseVoucher} = changeDateSlice.actions;

export default changeDateSlice.reducer;
