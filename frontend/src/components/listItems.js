import React from 'react';
import { Link } from 'react-router-dom';
import ListItem from '@material-ui/core/ListItem';
import ListItemIcon from '@material-ui/core/ListItemIcon';
import ListItemText from '@material-ui/core/ListItemText';
import ListSubheader from '@material-ui/core/ListSubheader';
import DashboardIcon from '@material-ui/icons/Dashboard';
import Announcement from '@material-ui/icons/Announcement';
// import BarChartIcon from '@material-ui/icons/BarChart';
import Settings from '@material-ui/icons/Settings';
import AssignmentIcon from '@material-ui/icons/Assignment';

export const mainListItems = (
  <div>
    <ListItem button component={Link}  to="/">

      <ListItemIcon>
        <DashboardIcon />
      </ListItemIcon>
      <ListItemText primary="Dashboard" />
    </ListItem>
    <ListItem button component={Link}  to="/errorlog">
      <ListItemIcon>
        <Announcement />
      </ListItemIcon>
      <ListItemText primary="Error Logs" />
    </ListItem>
    {/* <ListItem button>
      <ListItemIcon>
        <BarChartIcon />
      </ListItemIcon>
      <ListItemText primary="Reports" />
    </ListItem> */}
    <ListItem button component={Link}  to="/settings">
      <ListItemIcon>
        <Settings />
      </ListItemIcon>
      <ListItemText primary="Settings" />
    </ListItem>
  </div>
);

export const secondaryListItems = (
  <div>
    <ListSubheader inset>Saved reports</ListSubheader>
    <ListItem button component={Link}  to="/monthlyreport">
      <ListItemIcon>
        <AssignmentIcon />
      </ListItemIcon>
      <ListItemText primary="Current month" />
    </ListItem>
    {/* <ListItem button>
      <ListItemIcon>
        <AssignmentIcon />
      </ListItemIcon>
      <ListItemText primary="Last quarter" />
    </ListItem> */}
    <ListItem button component={Link}  to="/yearlyreport">
      <ListItemIcon>
        <AssignmentIcon />
      </ListItemIcon>
      <ListItemText primary="Last Year" />
    </ListItem>
  </div>
);
