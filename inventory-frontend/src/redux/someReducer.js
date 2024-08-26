const initialState = {
  value: 0,
};

function someReducer(state = initialState, action) {
  switch (action.type) {
    case 'INCREMENT':
      return { ...state, value: state.value + 1 };
    default:
      return state;
  }
}

export default someReducer;
