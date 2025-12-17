import React, { Dispatch, SetStateAction, useMemo } from 'react';
import { Box, Tooltip, Typography, Paper } from '@mui/material';
import { BlobIcon } from '../icons/BlobIcon';
import { useTranslation } from 'react-i18next';
import { PolicyType } from '../../../generated';
import { formatToShort } from '../../utils/sim-time-utils';
import { usePolicies } from '../../context/PoliciesContext';

export interface PolicyInfo {
  type: PolicyType;
  color: string;
  summary: string;
  name?: string; // Added name property
  effectUntil?: string;
}

const getPolicies = (): Pick<PolicyInfo, 'type' | 'color'>[] => {
  return [
    { type: 'FACTORY_MODERNIZATION', color: '#4caf50' },
    { type: 'GYM_IMPROVEMENT', color: '#2196f3' },
    { type: 'LABOUR_SUBSIDIES', color: '#ff9800' },
    { type: 'PENSION_SCHEME', color: '#9c27b0' },
  ];
};

export const PoliciesPanel = () => {
  const { t } = useTranslation();

  const { policies: policyData } = usePolicies();

  const policies = useMemo(
    () =>
      getPolicies().map((p) => {
        const activePolicy = policyData?.find((policy) => policy.type === p.type);

        const name = t(`policies.name.${p.type}`);
        const summary = t(`policies.summary.${p.type}`);

        return { ...p, effectUntil: activePolicy ? activePolicy.effectUntil : undefined, summary, name };
      }),
    [policyData],
  );

  return (
    <Box display="flex" flexDirection="row" gap={1} alignItems="center">
      {policies.map((p) => (
        <Tooltip
          key={p.type}
          title={
            <React.Fragment>
              <Typography sx={{ fontWeight: 700 }}>{p.name}</Typography>
              <Typography variant="body2">{p.summary}</Typography>
              {p.effectUntil ? (
                <Typography variant="caption" sx={{ display: 'block', marginTop: 0.5 }}>
                  {t('policies.effect_until', { effectUntil: formatToShort(p.effectUntil) })}
                </Typography>
              ) : null}
            </React.Fragment>
          }
          placement="top"
        >
          <Paper
            elevation={1}
            sx={{
              width: { xs: 40, xl: 50 },
              height: { xs: 40, xl: 50 },
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              borderRadius: 1,
              border: !p.effectUntil ? '1px dashed rgba(0,0,0,0.2)' : undefined,
              opacity: !p.effectUntil ? 0.5 : 1,
            }}
          >
            <BlobIcon size={28} color={!p.effectUntil ? '#bdbdbd' : p.color} />
          </Paper>
        </Tooltip>
      ))}
    </Box>
  );
};

export default PoliciesPanel;
