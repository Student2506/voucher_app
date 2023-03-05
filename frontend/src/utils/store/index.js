import { configureStore } from '@reduxjs/toolkit';
import userSlice from "./userSlice";
import customersSlice from "./customersSlice";

const store = configureStore({
  reducer: {
    user: userSlice,
    customers: customersSlice,
  },
})

export default store;
