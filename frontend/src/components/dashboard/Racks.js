import React from "react";
import Card from "@material-ui/core/Card";
import CardContent from "@material-ui/core/CardContent";
import CardHeader from "@material-ui/core/CardHeader";
import Grid from "@material-ui/core/Grid";
import Typography from "@material-ui/core/Typography";
import { makeStyles } from "@material-ui/core/styles";
import Container from "@material-ui/core/Container";
import Server from "./Server";

const useStyles = makeStyles((theme) => ({
    "@global": {
        ul: {
            margin: 0,
            padding: 0,
            listStyle: "none",
        },
    },
    heroContent: {
        padding: theme.spacing(8, 0, 6),
    },
    cardHeader: {
        backgroundColor:
            theme.palette.type === "dark"
                ? theme.palette.grey[700]
                : theme.palette.grey[200],
    },
}));

const tiers = [
    {
        title: "Rack 1",
        servers: [
            ["1", "r1_s1", "17.192.60.49", "Ubuntu 18.04", "83", "40"],
            ["2", "r1_s2", "235.206.163.213", "Windows 7", "76", "38"],
            ["3", "r1_s3", "31.48.70.92", "Windows 10", "49", "60"],
        ],
    },
    {
        title: "Rack 2",
        servers: [
            ["1", "r1_s1", "249.8.152.227", "Ubuntu 18.04", "82", "61"],
            ["2", "r1_s2", "8.220.11.103", "Windows 10", "27", "93"],
            ["3", "r1_s3", "38.192.127.154", "Windows 7", "44", "77"],
            ["4", "r1_s4", "22.74.368.15", "Ubuntu 16.04", "87", "37"],
        ],
    },
    {
        title: "Rack 3",
        servers: [
            ["1", "r1_s1", "106.7.151.150", "Windows 10", "93", "91"],
            ["2", "r1_s2", "174.185.160.163", "Ubuntu 18.04", "80", "64"],
            ["3", "r1_s3", "212.74.38.159", "Windows 7", "77", "87"],
        ],
    },
];
export default function Racks() {
    const classes = useStyles();
    fetch('http://127.0.0.1:5000/test', {
      method: 'GET',
      mode: 'cors',
      headers: {
        'Content-Type': 'application/json',
      },
    })
        .then((response) => response.json())
        .then((data) => {
            console.log(data);
        })
        .catch((error) => console.error(error));
    return (
        <React.Fragment>
            {/* Hero unit */}
            <Container
                maxWidth="sm"
                component="main"
                className={classes.heroContent}
            >
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
            <Container maxWidth="lg" component="main">
                <Grid container spacing={2}>
                    {tiers.map((tier) => (
                        <Grid item key={tier.title} xs={12} md={4}>
                            <Card>
                                <CardHeader
                                    title={tier.title}
                                    titleTypographyProps={{ align: "center" }}
                                    subheaderTypographyProps={{
                                        align: "center",
                                    }}
                                    className={classes.cardHeader}
                                />
                                <CardContent>
                                    <ul>
                                        {tier.servers.map((server) => (
                                            <React.Fragment>
                                                <Server
                                                    // expanded={true}
                                                    position={server[0]}
                                                    ip={server[2]}
                                                    os={server[3]}
                                                    cpu={server[4]}
                                                    dsk={server[5]}
                                                />
                                            </React.Fragment>
                                        ))}
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
