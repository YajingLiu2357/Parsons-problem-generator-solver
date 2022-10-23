import { createStore } from 'vuex'

export default createStore({
    state:{
        hello:'Vue-SPA-Quickstart',
        userStatus: 'visitor',  // visitor, student, teacher, admin
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
        chgActiveTab(state, payload){
            state.activeTab = tab;
            console.log('[debug] active tab change to ' +tab)
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