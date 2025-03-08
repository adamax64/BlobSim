import { Box } from "@mui/material";
import { ReactNode } from "react";

export function PageFrame({ children }: { children: ReactNode }) {
  return <Box display="flex" flexDirection="column" gap={2} className="p-2">
    {children}
  </Box>
}