import React from "react";
import Card from "@material-ui/core/Card";
import CardContent from "@material-ui/core/CardContent";
import CardHeader from "@material-ui/core/CardHeader";
import Grid from "@material-ui/core/Grid";
import Typography from "@material-ui/core/Typography";
import { makeStyles } from "@material-ui/core/styles";
import Container from "@material-ui/core/Container";
import Server from "./Server";

const useStyles = makeStyles(theme => ({
  "@global": {
    ul: {
      margin: 0,
      padding: 0,
      listStyle: "none"
    }
  },
  heroContent: {
    padding: theme.spacing(8, 0, 6)
  },
  cardHeader: {
    backgroundColor:
      theme.palette.type === "dark"
        ? theme.palette.grey[700]
        : theme.palette.grey[200]
  }
}));

const tiers = [
  {
    title: "Rack 1",
    servers: [
      ["1", "r1_s1", "Ubuntu 18.04", "83"],
      ["2", "r1_s2", "Windows 7", "83"],
      ["3", "r1_s3", "Windows 10", "83"]
    ]
  },
  {
    title: "Rack 2",
    servers: [
      ["1", "r1_s1", "Ubuntu 18.04", "83"],
      ["2", "r1_s2", "Windows 10", "83"],
      ["3", "r1_s3", "Windows 7", "83"]
    ]
  },
  {
    title: "Rack 3",
    servers: [
      ["1", "r1_s1", "Windows 10", "83"],
      ["2", "r1_s2", "Ubuntu 18.04", "83"],
      ["3", "r1_s3", "Windows 7", "83"]
    ]
  }
];
export default function Racks() {
  const classes = useStyles();
  return (
    <React.Fragment>
      {/* Hero unit */}
      <Container maxWidth="sm" component="main" className={classes.heroContent}>
        <Typography
          component="h1"
          variant="h2"
          align="center"
          color="textPrimary"
          gutterBottom
        >
          Data Center
        </Typography>
      </Container>
      {/* End hero unit */}
      <Container maxWidth="md" component="main">
        <Grid container spacing={5} alignItems="flex-end">
          {tiers.map(tier => (
            <Grid item key={tier.title} xs={12} md={4}>
              <Card>
                <CardHeader
                  title={tier.title}
                  titleTypographyProps={{ align: "center" }}
                  subheaderTypographyProps={{ align: "center" }}
                  className={classes.cardHeader}
                />
                <CardContent>
                  <ul>
                    {tier.servers.map(server => 
                        <React.Fragment>
                          <Server cpu={server[3]} />
                        </React.Fragment>
                    )}
                  </ul>
                </CardContent>
              </Card>
            </Grid>
          ))}
        </Grid>
      </Container>
    </React.Fragment>
  );
}
