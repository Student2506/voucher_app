import { createSlice } from "@reduxjs/toolkit";

const statusAppSlice = createSlice({
  name: 'statusApp',
  initialState: {
    status: null,
    error: null,
  },
  reducers: {
    rejectFetch(state, action) {
      state.status = 'rejected';
      state.error = action.payload;
    },
    fulfilledFetch(state, action) {
      state.status = 'resolved';
      state.error = null;
    },
    pendingFetch(state, action) {
      state.status = 'loading';
      state.error = null;
    },
    clearError(state) {
      state.error = null;
    }
  }
})

export const { rejectFetch, fulfilledFetch, pendingFetch } = statusAppSlice.actions;

export default statusAppSlice.reducer;
