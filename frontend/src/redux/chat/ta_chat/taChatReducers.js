import {
  FETCH_CHATDATA,
  FETCH_CHATDATA_REQUEST,
  FETCH_CHATDATA_SUCCESS,
  FETCH_CHATDATA_FAILURE,
  ADD_TA_CHATMSG,
  ADD_TA_CHATROOM,
  GET_TA_RESPONSE,
  CHANGE_NOW_TA_CHATROOM,
  CLEAR_TACHAT_LIST,
  CLEAR_TACHATROOM_LIST
} from './taChatTypes';

const initialState = {
  num: 0,
  roomNum: 0,
  nowRoomId: -1,
  chats: [
    // ex
    // {
    //   id: 1,
    //   name : '정상뷰'
    //   userId: 123,
    //   msg: '질문있습니다. 조교님.',
    //   time: 11/01 12:11
    // },
    // {
    //   id: 2,
    //   name : '정상뷰'
    //   userId: 123,
    //   sender: 'ta',
    //   msg: '넵넵ㅎㅎ',
    // },
  ],
  list: [
    // ex
    // {
    //   id: 2,
    //   roomId: 3,
    //   title: '알고리즘 및 실습',
    //   des: '홍길동 교수 / TA 정성벽',
    // },
  ],
};

const taChatReducer = (state = initialState, action) => {
  const { type, data } = action;

  switch (type) {
    case FETCH_CHATDATA_SUCCESS:
      return state;

    case CLEAR_TACHAT_LIST:
      return {
        ...state,
        chats: [],
        num: 0,
      }

    case CLEAR_TACHATROOM_LIST:
      return {
        ...state,
        list: [],
        nowRoomId:-1,
        roomNum: 0,
      }

    case ADD_TA_CHATMSG:
      //state.num= state.num + 1;
      return {
        ...state,
        chats: state.chats.concat({
          id: state.num + 1,
          name: data.name,
          userId: data.userId,
          msg: data.msg,
          time:data.time,
        }),
        num: state.num + 1,
      };

    case CHANGE_NOW_TA_CHATROOM:
      return {
        ...state,
        nowRoomId: data.nowRoomId,
      }

    case ADD_TA_CHATROOM:
      return {
        ...state,
        list: state.list.concat({
          id: state.roomNum + 1,
          roomId: data.roomId,
          title: data.title,
          des: data.des,
        }),
        roomNum: state.roomNum + 1,
      };

    default:
      return state;
  }
};

export default taChatReducer;
