"""add interview tables

Revision ID: 6dd9501f3c90
Revises: 5dd9501f3c89
Create Date: 2026-03-20 10:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6dd9501f3c90'
down_revision: Union[str, None] = '5dd9501f3c89'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 创建面试题库表
    op.create_table(
        'interview_questions',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('category', sa.String(50), nullable=False),
        sa.Column('job_type', sa.String(50), nullable=True),
        sa.Column('question_text', sa.Text(), nullable=False),
        sa.Column('reference_answer', sa.Text(), nullable=True),
        sa.Column('scoring_criteria', sa.JSON(), nullable=True),
        sa.Column('difficulty', sa.String(20),
                  server_default='medium', nullable=True),
        sa.Column('tags', sa.JSON(), nullable=True),
        sa.Column('question_order', sa.Integer(),
                  server_default='0', nullable=True),
        sa.Column('is_active', sa.Boolean(),
                  server_default='true', nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_interview_questions_id'),
                    'interview_questions', ['id'], unique=False)

    # 创建面试会话表
    op.create_table(
        'interview_sessions',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('interview_mode', sa.String(50), nullable=False),
        sa.Column('target_job', sa.String(100), nullable=True),
        sa.Column('status', sa.String(20),
                  server_default='pending', nullable=True),
        sa.Column('total_score', sa.Float(),
                  server_default='0', nullable=True),
        sa.Column('overall_feedback', sa.Text(), nullable=True),
        sa.Column('strengths', sa.JSON(), nullable=True),
        sa.Column('improvements', sa.JSON(), nullable=True),
        sa.Column('duration', sa.Integer(), server_default='0', nullable=True),
        sa.Column('started_at', sa.DateTime(), nullable=True),
        sa.Column('completed_at', sa.DateTime(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_interview_sessions_id'),
                    'interview_sessions', ['id'], unique=False)

    # 创建面试回答表
    op.create_table(
        'interview_answers',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('session_id', sa.Integer(), nullable=False),
        sa.Column('question_id', sa.Integer(), nullable=False),
        sa.Column('user_answer', sa.Text(), nullable=True),
        sa.Column('score', sa.Float(), server_default='0', nullable=True),
        sa.Column('score_details', sa.JSON(), nullable=True),
        sa.Column('feedback', sa.Text(), nullable=True),
        sa.Column('suggestions', sa.Text(), nullable=True),
        sa.Column('answer_duration', sa.Integer(),
                  server_default='0', nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(
            ['session_id'], ['interview_sessions.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(
            ['question_id'], ['interview_questions.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_interview_answers_id'),
                    'interview_answers', ['id'], unique=False)

    # 创建岗位信息表
    op.create_table(
        'job_positions',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(100), nullable=False),
        sa.Column('code', sa.String(50), nullable=False),
        sa.Column('logo', sa.String(10), nullable=True),
        sa.Column('question_count', sa.Integer(),
                  server_default='0', nullable=True),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('is_hot', sa.Boolean(),
                  server_default='false', nullable=True),
        sa.Column('is_active', sa.Boolean(),
                  server_default='true', nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('code')
    )
    op.create_index(op.f('ix_job_positions_id'),
                    'job_positions', ['id'], unique=False)


def downgrade() -> None:
    op.drop_index(op.f('ix_job_positions_id'), table_name='job_positions')
    op.drop_table('job_positions')

    op.drop_index(op.f('ix_interview_answers_id'),
                  table_name='interview_answers')
    op.drop_table('interview_answers')

    op.drop_index(op.f('ix_interview_sessions_id'),
                  table_name='interview_sessions')
    op.drop_table('interview_sessions')

    op.drop_index(op.f('ix_interview_questions_id'),
                  table_name='interview_questions')
    op.drop_table('interview_questions')
