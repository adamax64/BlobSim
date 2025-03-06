import { Box, Button, Card, CardContent, CardHeader, Typography } from "@mui/material";
import { BlobIcon } from "./BlobIcon";
import { useMutation } from "@tanstack/react-query";
import defaultConfig from "../default-config";
import { GeneralInfosApi, News, NewsType, SimDataApi } from "../../generated";
import { useEffect, useMemo } from "react";
import { AddCircle, SkipNext, Stadium } from "@mui/icons-material";
import { PageTitleCard } from "./PageTitleCard";

function isDigit(char: string) {
  return char >= '0' && char <= '9'
}

function getNewsText(news: News) {
  switch (news.newsType) {
    case NewsType.Event:
      return "There is a championship event today!"
    case NewsType.BlobCreatedAndNamed:
      return `A new blob called ${news.additionalInfo} has been created!`
    case NewsType.BlobCreated:
      return "A new blob has been created!"
    case NewsType.SeasonStart:
      return "A new season has started!"
    case NewsType.Continue:
      return "Nothing special happening today"
  }
}

export function DashboardPage() {
  const simDataApi = new SimDataApi(defaultConfig);
  const generalApi = new GeneralInfosApi(defaultConfig);

  const { data: simTime, mutate: getSimTime } = useMutation<string, Error>({ mutationFn: () => simDataApi.getSimTimeSimDataSimTimeGet() })
  const { data: news, mutate: getNews } = useMutation<News[], Error>({ mutationFn: () => generalApi.getEventSpecificOptionsGeneralInfosNewsGet() })

  useEffect(() => {
    getSimTime()
    getNews()
  }, [])

  const newsTypes: NewsType[] = useMemo(() => news?.map(newsItem => newsItem.newsType) || [], [news])

  return (
    <Box display="flex" flexDirection="column" gap={2} className="p-2">
      <PageTitleCard title="Blob Championship System - Dashboard" />
      <Card>
        <CardContent>
          <Box display="flex" flexDirection="column" gap={1}>
            <Typography variant="h6">Date</Typography>
            <Box display="flex" gap={0}>
              {simTime ? simTime.split('').map((char, index) => isDigit(char)
                ? <Card key={index} className="p-2" sx={{ fontWeight: "600" }}>{char}</Card>
                : <Box key={index} className="p-1 pt-2" sx={{ fontWeight: "600" }}>{char}</Box>)
                : "Loading..."}
            </Box>
          </Box>
        </CardContent>
      </Card>
      <Card>
        <CardContent>
          <Box display="flex" flexDirection="column" gap={1}>
            <Typography variant="h6">News</Typography>
            {news ? news.map((newsItem, index) => <Box key={index} display="flex" flexDirection="column" gap={1}>
              <Typography variant="body1">{getNewsText(newsItem)}</Typography>
            </Box>) : "Loading..."}
          </Box>
        </CardContent>
      </Card>
      <Box display="flex" gap={1}>
        {newsTypes.includes(NewsType.Event) && <Button variant="contained" color="primary" endIcon={<Stadium />}>Proceed to event</Button>}
        {newsTypes.includes(NewsType.BlobCreated) && <Button variant="contained" color="primary" endIcon={<AddCircle />}>Create new Blob</Button>}
        {newsTypes.includes(NewsType.Continue) && <Button variant="contained" color="primary" endIcon={<SkipNext />}>Proceed to next day</Button>}
      </Box>
    </Box>
  )
}