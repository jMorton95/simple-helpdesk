from simple_kanban.tests.integration.base import BaseIntegrationTest
from simple_kanban.models import TicketComment

class TicketCommentIntegrationTests(BaseIntegrationTest):
  def test_create_ticket_with_comments(self):
    """
      Test creating comments for an existing ticket using the BaseIntegrationTest setup.
    """
    print("Testing Ticket Creation with Comments")

    comment1 = TicketComment.objects.create(
        text="This is a comment by user1.",
        parent_ticket=self.ticket1,
        user=self.user1,
        created_by=self.user1,
    )
    comment2 = TicketComment.objects.create(
        text="This is a comment by user2.",
        parent_ticket=self.ticket1,
        user=self.user2,
        created_by=self.user2,
    )

    #Assert
    self.assertEqual(self.ticket1.comments.count(), 2, "There should be exactly 2 comments on ticket1.")
    self.assertEqual(comment1.text, "This is a comment by user1.", "Comment1 text should match.")
    self.assertEqual(comment2.user, self.user2, "Comment2 should be made by user2.")

    print("Assertions Passed!")
