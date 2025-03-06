import { Box, Card, CardHeader } from "@mui/material";
import { BlobIcon } from "./BlobIcon";

interface PageTitleCardProps {
  title: string;
  blobIconColor?: string;
}

export function PageTitleCard({ title, blobIconColor }: PageTitleCardProps) {
  return <Card>
    <CardHeader title={
      <Box display="flex" gap={2}>
        <BlobIcon size={32} color={blobIconColor ?? `#${Math.floor(Math.random() * 16777215).toString(16)}`} />
        {title}
      </Box>
    } />
  </Card>
}