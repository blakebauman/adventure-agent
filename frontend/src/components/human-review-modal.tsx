import { useState } from 'react';
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from './ui/dialog';
import { Button } from './ui/button';
import { Input } from './ui/input';

interface HumanReviewModalProps {
  onReview: (
    status: 'approved' | 'rejected' | 'needs_revision',
    feedback: string
  ) => void;
  onClose: () => void;
}

export function HumanReviewModal({
  onReview,
  onClose,
}: HumanReviewModalProps) {
  const [feedback, setFeedback] = useState('');

  const handleSubmit = (status: 'approved' | 'rejected' | 'needs_revision') => {
    onReview(status, feedback);
    setFeedback('');
  };

  return (
    <Dialog open={true} onOpenChange={onClose}>
      <DialogContent>
        <DialogHeader>
          <DialogTitle>Review Adventure Plan</DialogTitle>
          <DialogDescription>
            Please review the adventure plan and provide feedback if needed.
          </DialogDescription>
        </DialogHeader>
        <div className="space-y-4">
          <div>
            <label className="text-sm font-medium">Feedback (optional)</label>
            <Input
              value={feedback}
              onChange={(e) => setFeedback(e.target.value)}
              placeholder="Enter any feedback or changes you'd like..."
              className="mt-2"
            />
          </div>
        </div>
        <DialogFooter className="flex gap-2">
          <Button
            variant="outline"
            onClick={() => handleSubmit('rejected')}
          >
            Reject
          </Button>
          <Button
            variant="outline"
            onClick={() => handleSubmit('needs_revision')}
          >
            Needs Revision
          </Button>
          <Button onClick={() => handleSubmit('approved')}>
            Approve
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
}

