// import React from 'react';

// export default function App() {
//   return (
//     <Dashboard />
//   );
// }
import React from "react";
import { BrowserRouter as Router, Switch, Route } from "react-router-dom";
import history from "./util/history.js";
// import { withStore } from "react-context-hook";
import Dashboard from './components/Dashboard';
import ErrorLog from './components/ErrorLog';
import MonthlyReport from './components/MonthlyReport';
import YearlyReport from './components/YearlyReport';
import Settings from './components/Settings';


// const initialState = Object.assign(
//     {
//         isLoggedIn: false,
//         username: null,
//     },
//     JSON.parse(localStorage.getItem("state"))
// ); // Using localStorage to persist on reload

// const storeConfig = {
//     listener: (state) => {
//         console.log("state changed", state);
//         // persist state to localStorage
//         localStorage.setItem("state", JSON.stringify(state));
//     },
//     logging: process.env.NODE_ENV !== "production",
// };

function App() {
    return (
        <Router history={history}>
            <Switch>
                <Route exact path="/" component={Dashboard} />
                <Route exact path="/errorlog" component={ErrorLog} />
                <Route exact path="/monthlyreport" component={MonthlyReport} />
                <Route exact path="/yearlyreport" component={YearlyReport} />
                <Route exact path="/settings" component={Settings} />
            </Switch>
        </Router>
    );
}

// export default withStore(App, initialState, storeConfig);
export default App;