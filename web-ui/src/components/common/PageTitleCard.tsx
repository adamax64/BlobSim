import { Box, Card, CardHeader } from "@mui/material";
import { BlobIcon } from "../icons/BlobIcon";
import { useMemo } from "react";

interface PageTitleCardProps {
  title: string;
  blobIconColor?: string;
  center?: boolean;
}

export function PageTitleCard({ title, blobIconColor, center }: PageTitleCardProps) {
  const iconColor = useMemo(() => blobIconColor ?? `#${Math.floor(Math.random() * 16777215).toString(16)}`, [blobIconColor])

  return <Card>
    <CardHeader title={
      <Box display="flex" gap={2} justifyContent={center ? "space-between" : "start"}>
        <BlobIcon size={32} color={iconColor} />
        {title}
        <BlobIcon size={32} color={iconColor} />
      </Box>
    } />
  </Card>
}