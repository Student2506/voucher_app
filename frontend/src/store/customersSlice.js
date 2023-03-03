import {createSlice, createAsyncThunk} from "@reduxjs/toolkit";
import { baseUrl } from "../constants";

export const getCustomers = createAsyncThunk(
  'customers/getCustomers',
  async function(_, {rejectWithValue, dispatch, getState}) {
    const jwt = getState().user.userData.jwt.auth;
    try {
      const res = await fetch(`${baseUrl}/api/v1/customers/`, {
        method: 'GET',
        headers: {
          "Content-Type": "application/json",
          "Authorization": `JWT ${jwt}`,
        }
      })
      if (!res.ok) throw new Error(`Ошибка при получении данных`);
      const data = await res.json();
      dispatch(addCustomers({data}))
    } catch (err) {
      return rejectWithValue(err);
    }
  }
)

export const getCustomerOrders = createAsyncThunk(
  'customers/getCustomerOrders',
  async function({ id }, {rejectWithValue, dispatch, getState}) {
    const jwt = getState().user.userData.jwt.auth;
    try {
      const res = await fetch(`${baseUrl}/api/v1/customers/${id}/`, {
        method: 'GET',
        headers: {
          "Content-Type": "application/json",
          "Authorization": `JWT ${jwt}`,
        }
      })
      if (!res.ok) throw new Error(`Ошибка при получении данных`);
      const data = await res.json();
      dispatch(addOrders({data}))
    } catch (err) {
      return rejectWithValue(err);
    }
  }
)

export const getOrderTemplates = createAsyncThunk(
  'customers/getOrderTemplates',
  async function({id}, {rejectWithValue, dispatch, getState}) {
    const jwt = getState().user.userData.jwt.auth;
    try {
      const res = await fetch(`${baseUrl}/api/v1/voucher_type/${id}`, {
        method: 'GET',
        headers: {
          "Content-Type": "application/json",
          "Authorization": `JWT ${jwt}`,
        }
      })
      if (!res.ok) throw new Error(`Ошибка при получении данных`);
      const data = await res.json();
      dispatch(addTemplates({data}))
    } catch (err) {
      return rejectWithValue(err);
    }
  }
)

export const customersSlice = createSlice({
  name: 'customers',
  initialState: {
    customers: [],
    orders: [],
    templates: [],
  },
  reducers: {
    addCustomers(state, action) {
      state.customers = action.payload.data.results;
    },
    addOrders(state, action) {
      state.orders = action.payload.data.orders;
    },
    addTemplates(state, action) {
      state.templates = Object.entries(action.payload.data.templates).map((e) => ( { [e[0]]: e[1] } ));
    }
  }
})

export const {addCustomers, addOrders, addTemplates} = customersSlice.actions;

export default customersSlice.reducer;
