import {createSlice, createAsyncThunk} from "@reduxjs/toolkit";
import {BASE_URL} from "../../constants";

export const getTemplates = createAsyncThunk(
  'templates/getTemplates',
  async function(_, {rejectWithValue, dispatch, getState}) {
    const jwt = getState().user.userData.jwt.auth;
    try {
      const res = await fetch(`${BASE_URL}/api/v1/templates`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          "Authorization": `JWT ${jwt}`,
        }
      })
      if(!res.ok) throw new Error('Произошла ошибка')
      const data = await res.json();
      dispatch(addTemplates(data.results));
    } catch (err) {
      return rejectWithValue(err.message);
    }
  }
)

export const updateTemplate = createAsyncThunk(
  'templates/updateTemplate',
  async function(newTextForTemplate, {rejectWithValue, dispatch, getState}) {
    const jwt = getState().user.userData.jwt.auth;
    try {
      const res = await fetch(`${BASE_URL}/api/v1/templates/${newTextForTemplate.id}/`, {
        method: 'PATCH',
        headers: {
          'Content-Type': 'application/json',
          "Authorization": `JWT ${jwt}`,
        },
        body: JSON.stringify({
          title: newTextForTemplate.title,
          template_property: newTextForTemplate.template_property,
        })
      })
      if(!res.ok) throw new Error('Произошла ошибка')
      const data = await res.json();
      dispatch(patchTemplate(data))
    } catch (err) {
      return rejectWithValue(err.message);
    }
  }
)

export const templatesSlice = createSlice({
  name: 'templates',
  initialState: {
    templates: [],
    status: null,
  },
  reducers: {
    addTemplates(state, action) {
      state.templates = action.payload;
      console.log(action.payload);
    },
    patchTemplate(state, action) {
      let editedTemplate = state.templates.find(template => template.id === action.payload.id);
      editedTemplate = action.payload
    },
    dropStatus(state) {
      state.status = null;
    }
  },
  extraReducers: {
    [getTemplates.pending]: (state) => {
      state.status = 'loading';
    },
    [getTemplates.fulfilled]: (state) => {
      state.status = null;
    },
    [getTemplates.rejected]: (state, action) => {
      state.status = 'rejected';
    },
    [updateTemplate.rejected]: (state) => {
      state.status = 'rejected';
    },
    [updateTemplate.fulfilled]: (state) => {
      state.status = 'resolved';
    },
    [updateTemplate.pending]: (state) => {
      state.status = null;
    },
  }
})

export const {addTemplates, patchTemplate, dropStatus} = templatesSlice.actions;

export default templatesSlice.reducer;

