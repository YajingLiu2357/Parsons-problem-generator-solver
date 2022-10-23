import { createStore } from 'vuex'

export default createStore({
    state:{
        hello:'Vue-SPA-Quickstart',
        userStatus: 'teacher',  // visitor, student, teacher, admin
        activeTab: '',
        userEmail: '',
        userName: '',
        UID: '',
    },
    mutations: {
        chgUser(state, payload){
            state.UID = payload.UID;
            state.userEmail = payload.userEmail;
            state.userName = payload.userName;
        },
        chgStatus(state, payload){
            state.userStatus = payload.userStatus;
        },
        signOut(state){
            state.UID = '';
            state.userEmail = '';
            state.userName = '';
            state.activeTab = '';
            state.userStatus = 'visitor';
        },
    },
    actions: {}
})